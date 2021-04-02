package cn.toesbieya.jxc.service.doc;

import cn.toesbieya.jxc.constant.ProductConstants;
import cn.toesbieya.jxc.mapper.ProductExportMapper;
import cn.toesbieya.jxc.model.entity.ProductExportRecord;
import cn.toesbieya.jxc.model.vo.R;
import cn.toesbieya.jxc.model.vo.result.PageResult;
import cn.toesbieya.jxc.model.vo.search.ProductExport;
import cn.toesbieya.jxc.util.DateUtil;
import cn.toesbieya.jxc.util.FileUtils;
import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.toolkit.CollectionUtils;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.github.pagehelper.PageHelper;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.UUID;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * The type Product export service.
 */
@Service
@Slf4j
public class ProductExportService {

    private static ThreadPoolExecutor executor;

    static {
        executor = new ThreadPoolExecutor(1, 10, 10, TimeUnit.SECONDS,
                new LinkedBlockingQueue<>());
        executor.prestartAllCoreThreads();
    }


    /**
     * The Product export mapper.
     */
    @Resource
    ProductExportMapper productExportMapper;

    /**
     * Submit page result.
     *
     * @param vo the vo
     * @return the page result
     */
    public PageResult<ProductExportRecord> submit(ProductExport vo) {
        PageHelper.startPage(vo.getPage(), vo.getPageSize());
        insert(vo);
        return new PageResult<>(productExportMapper.queryAll(getSearchCondition(vo)));
    }

    private void collectProduct(ProductExportRecord productExportRecord) {
        executor.execute(() -> {
            String fileName = productExportRecord.getId() + ProductConstants.Suffix.SHOPIFY_SUFFIX;
            String res = FileUtils.collectProducts(productExportRecord.getLinkUrl(), fileName, productExportRecord.getProductExport());
            boolean exportResult = StringUtils.contains(res, "success");
            String pythonProductNumber = StringUtils.substringAfterLast(res, "product_num");
            Long productNumber = exportResult && StringUtils.isNumeric(pythonProductNumber) ? Long.parseLong(pythonProductNumber) : 0L;
//            productExportMapper.updateStatusAndProductNumberAndExportFileById(exportResult ? ProductConstants.ExportStatus.SUCCESS : ProductConstants.ExportStatus.FAIL,
//                    productNumber, fileName, uuid);
            ProductExportRecord record = new ProductExportRecord();
            String endTime = DateUtil.dateFormat();
            record.setUpdateTime(endTime);
            record.setExportFile(fileName);
            record.setStatus(exportResult ? ProductConstants.ExportStatus.SUCCESS : ProductConstants.ExportStatus.FAIL);
            record.setProductNumber(productNumber);
            record.setFileContent(FileUtils.getFileContent(fileName));
            record.setDuration(DateUtil.getDuration(productExportRecord.getExportTime(), endTime));
            productExportMapper.updateById(record, productExportRecord.getId());
        });
    }


    private void insert(ProductExport vo) {
        String linkUrl = StringUtils.EMPTY;
        if (StringUtils.isNotEmpty(vo.getCollectionUrl())) {
            linkUrl = vo.getCollectionUrl().replace("，", ProductConstants.URL_SEPARATOR);
        } else if (CollectionUtils.isNotEmpty(vo.getProductUrlList())) {
            linkUrl = StringUtils.join(vo.getProductUrlList(), ProductConstants.URL_SEPARATOR);
        }
        if (StringUtils.isEmpty(linkUrl)) {
            return;
        }
        ProductExportRecord exportRecord = new ProductExportRecord();
        exportRecord.setId(UUID.randomUUID().toString());
        exportRecord.setLinkUrl(linkUrl);
        exportRecord.setFromSite(vo.getFromSite());
        String startTime = DateUtil.dateFormat();
        exportRecord.setExportTime(startTime);
        exportRecord.setStatus(ProductConstants.ExportStatus.WAITING);
        exportRecord.setProductNumber(vo.getMaxProductSize() == null ? 0L : vo.getMaxProductSize());
        exportRecord.setProductExport(vo.getProductExport() != null && vo.getProductExport() ? ProductConstants.YES : ProductConstants.NO);
        productExportMapper.insertSelective(exportRecord);
        collectProduct(exportRecord);
    }

    private Wrapper<ProductExportRecord> getSearchCondition(ProductExport vo) {
        return Wrappers.lambdaQuery(ProductExportRecord.class)
                .eq(ProductExportRecord::getVisible, ProductConstants.Visible.YES)
                .eq(vo.getProductExport() != null, ProductExportRecord::getProductExport, vo.getProductExport() != null && vo.getProductExport() ? ProductConstants.YES : ProductConstants.NO)
                .eq(StringUtils.isNotEmpty(vo.getFromSite()), ProductExportRecord::getFromSite, vo.getFromSite()).orderByDesc(ProductExportRecord::getExportTime);
    }

    /**
     * Del r.
     *
     * @param recordId the record id
     * @return the r
     */
    public R del(String recordId) {
        if (productExportMapper.updateVisibleById(ProductConstants.Visible.NO, recordId) < 1) {
            return R.fail("删除失败");
        }
        return R.success("删除成功");
    }
}

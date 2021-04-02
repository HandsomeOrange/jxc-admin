package cn.toesbieya.jxc.service;


import cn.toesbieya.jxc.constant.ProductConstants;
import cn.toesbieya.jxc.mapper.ProductExportMapper;
import cn.toesbieya.jxc.model.entity.ProductExportRecord;
import org.apache.commons.lang3.StringUtils;
import org.apache.poi.util.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletResponse;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Base64;

@Service
public class FileDownloadService {


    private static final Logger LOGGER = LoggerFactory.getLogger(FileDownloadService.class);

    @Resource
    ProductExportMapper productExportMapper;


    public void downloadWithFileName(String recordId, HttpServletResponse response) {
        LOGGER.info("record id {} start to download >>> ", recordId);
        if (StringUtils.isEmpty(recordId)) {
            return;
        }
        ProductExportRecord exportRecord = productExportMapper.selectById(recordId);
        if (exportRecord == null || ProductConstants.ExportStatus.SUCCESS != exportRecord.getStatus() || StringUtils.isEmpty(exportRecord.getFileContent())) {
            LOGGER.error("record id {} cant be download >>> ", recordId);
            return;
        }
        writeStringToResponse(exportRecord.getFileContent(), response);
    }


    private void writeStringToResponse(String data, HttpServletResponse response) {
        try (InputStream inputStream = new ByteArrayInputStream(Base64.getDecoder().decode(data));
             OutputStream outputStream = response.getOutputStream()) {
            response.reset();
            response.setContentType("application/x-download;charset=GBK");
            response.setHeader("Content-Disposition", "attachment;filename=x.x");
            IOUtils.copy(inputStream, outputStream);
            outputStream.flush();
        } catch (Exception e) {
            LOGGER.error("write file error ", e);
        }
    }
}

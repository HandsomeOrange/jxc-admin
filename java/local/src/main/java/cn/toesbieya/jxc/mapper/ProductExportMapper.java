package cn.toesbieya.jxc.mapper;

import cn.toesbieya.jxc.model.entity.ProductExportRecord;
import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.toolkit.Constants;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface ProductExportMapper extends BaseMapper<ProductExportRecord> {

    List<ProductExportRecord> queryAll(@Param(Constants.WRAPPER) Wrapper<ProductExportRecord> wrapper);

    ProductExportRecord selectById(@Param("id")String id);

    void insertRecord(ProductExportRecord productExportRecord);

    int updateStatusAndProductNumberById(@Param("updatedStatus") Integer updatedStatus, @Param("updatedProductNumber") Long updatedProductNumber, @Param("id") String id);

    int updateStatusAndProductNumberAndExportFileById(@Param("updatedStatus") Integer updatedStatus, @Param("updatedProductNumber") Long updatedProductNumber, @Param("updatedExportFile") String updatedExportFile, @Param("id") String id);


    int updateStatusAndProductNumberAndExportFileAndFileContentAndUpdateTimeById(@Param("updatedStatus")Integer updatedStatus,@Param("updatedProductNumber")Long updatedProductNumber,@Param("updatedExportFile")String updatedExportFile,@Param("updatedFileContent")String updatedFileContent,@Param("updatedUpdateTime")String updatedUpdateTime,@Param("id")String id);

    int updateVisibleById(@Param("updatedVisible")Integer updatedVisible,@Param("id")String id);

    int updateById(@Param("updated")ProductExportRecord updated,@Param("id")String id);

    int insertSelective(ProductExportRecord productExportRecord);







}

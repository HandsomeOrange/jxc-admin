package cn.toesbieya.jxc.model.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import lombok.ToString;

@Data
@ToString(callSuper = true)
@TableName("export_history")
public class ProductExportRecord {
    private String id;
    private String linkUrl;
    private String fromSite;
    private String exportTime;
    private String updateTime;
    private String exportFile;
    private Integer status;
    private Long productNumber;
    private String fileContent;
    private Integer visible;
    private Long duration;
    private Integer productExport;
}

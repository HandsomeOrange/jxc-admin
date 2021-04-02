package cn.toesbieya.jxc.model.vo.search;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

import java.util.List;

@Data
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
public class ProductExport extends BaseSearch {

    private String collectionUrl;

    private List<String> productUrlList;

    private String fromSite;

    private Integer maxProductSize;

    private Boolean productExport;
}

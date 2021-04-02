package cn.toesbieya.jxc.controller.doc;

import cn.toesbieya.jxc.model.vo.R;
import cn.toesbieya.jxc.model.vo.search.ProductExport;
import cn.toesbieya.jxc.service.doc.ProductExportService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;

@RestController
@RequestMapping("/shopify")
public class ShopifyController {

    private static final Logger logger = LoggerFactory.getLogger(ShopifyController.class);

    @Resource
    private ProductExportService service;

    @PostMapping("/submit")
    public R submit(@RequestBody ProductExport productExport) {
        logger.info("shopify export param: {}",productExport);
        return R.success(service.submit(productExport));
    }

    @GetMapping("/del")
    public R del(@RequestParam String id) {
        if (StringUtils.isEmpty(id)) return R.fail("参数错误");
        return service.del(id);
    }

}

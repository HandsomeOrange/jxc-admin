package cn.toesbieya.jxc.controller.doc;

import cn.toesbieya.jxc.service.FileDownloadService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletResponse;

@RestController
public class DownloadController {

    @Resource
    FileDownloadService fileDownloadService;


    @RequestMapping(path = "/download/by-id", method = RequestMethod.GET)
    public void downloadWithFileName(@RequestParam(name = "id") String recordId, HttpServletResponse response) {
        fileDownloadService.downloadWithFileName(recordId, response);
    }


}

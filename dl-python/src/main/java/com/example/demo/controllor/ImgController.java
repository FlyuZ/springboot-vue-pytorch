package com.example.demo.controllor;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ImgController {
    ImgUtils imgUtils;
    @RequestMapping(value = "/api/getimg", method= RequestMethod.GET) //前端api接口
    public String stringetimg() {
        String base64 = "";
        do {
            if (!imgUtils.queue.isEmpty())
                base64 = imgUtils.queue.poll();
        } while (base64.isEmpty());
        System.out.println(imgUtils.queue.size());
        return base64;
    }
    @RequestMapping(value = "/api/initdl", method= RequestMethod.GET) //前端api接口
    public String initDl() {
        imgUtils = new ImgUtils();
        imgUtils.getImg("./sheep2.mp4");
        return "success";
    }
    @RequestMapping(value = "/test", method= RequestMethod.GET)
    public String test() {
        return "success";
    }
}

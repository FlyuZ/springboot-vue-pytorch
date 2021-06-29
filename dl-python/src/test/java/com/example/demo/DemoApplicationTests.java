package com.example.demo;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

@SpringBootTest
class DemoApplicationTests {
    private  final  static String url =  "http://localhost:9000";
    private static RestTemplate restTemplate = new RestTemplate();


    @Test
    void contextLoads() {
        ResponseEntity<String> response = restTemplate.exchange(url + "/test" ,
                HttpMethod.GET,
                new HttpEntity(null),
                String.class);
        System.out.println("result: " + response.getBody());
    }

}

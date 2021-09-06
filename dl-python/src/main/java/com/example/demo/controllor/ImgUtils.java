package com.example.dlface.controllor;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;
import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

public class ImgUtils{
    public ConcurrentLinkedQueue<String> queue;

    public void getImg(String imgPath) {
        Socket socket = null;
        Thread thread = null;
        queue = new ConcurrentLinkedQueue<>();
        try {
            InetAddress addr = InetAddress.getLocalHost();
            String host = addr.getHostAddress();
            System.out.println(host);
            // 初始化套接字，设置访问服务的主机和进程端口号，HOST是访问python进程的主机名称，可以是IP地址或者域名，PORT是python进程绑定的端口号
            socket = new Socket(host, 8888);
            System.out.println(socket.isConnected());

            // 获取输出流对象
            OutputStream os = socket.getOutputStream();
            PrintStream out = new PrintStream(os);
            // 发送内容
            out.print(imgPath);
            // 告诉服务进程，内容发送完毕，可以开始处理
            out.print("over");
            // 获取服务进程的输入流
            InputStream is = socket.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(is,"utf-8"));
            Runnable task = new Runnable() {
                @Override
                public void run() { // 覆盖重写抽象方法
                    String tmp = null;
                    while(true) {
                        try {
                            if ((tmp = br.readLine()) == null) break;
                            if(tmp.length() < 10)
                                continue;
                            System.out.println(tmp.length());
                            queue.offer(tmp);
                            Thread.sleep(30);
                        } catch (IOException | InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
            };
            thread = new Thread(task); // 启动线程
            thread.start();
        } catch (IOException  e) {
            e.printStackTrace();
        }  finally {
            System.out.println("远程接口正在调用.");
        }
    }
}
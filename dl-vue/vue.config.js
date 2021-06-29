module.exports = {
    devServer: {
        open: true,
        host:'0.0.0.0',
        port: 8090,
        proxy: {
            '/api': {
                target: 'http://localhost:9000',
                ws: true,
                changeOrigin: true,
                // pathRewrite: {
                //     "^/api": "" //请求的时候使用这个api就可以
                //   }
            },
        }
    }
}
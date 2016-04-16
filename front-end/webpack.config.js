var path = require('path'),
    fs   = require('fs'),
    glob = require('glob'),
    srcDir = './',
    entriesDir = 'entries/';

function getEntry () {
    var entry = {};

    glob.sync(srcDir + entriesDir + '**/*.*').forEach(function (name) {
        var n = name.slice(name.lastIndexOf(entriesDir) + entriesDir.length, name.lastIndexOf('.'));
        entry[n] = name;
    });
    return entry; 
};

module.exports = {
    devtool: "source-map",    //生成sourcemap,便于开发调试
    entry: getEntry(),         //获取项目入口js文件
    output: {
        path: path.join(__dirname, "dest/"), //文件输出目录
        //publicPath: "dist/js/",        //用于配置文件发布路径，如CDN或本地服务器
        filename: "[name].js",        //根据入口文件输出的对应多个文件名
    },
    module: {
        loaders: [{
            test: /\.vue$/,
            loader: 'vue',
        }, {
            test: /\.es6$/,
            loader: 'babel',
            query: {
                presets: ['es2015']
            }
        }]
    }
};
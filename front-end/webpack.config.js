var path = require('path'),
    precss = require('precss'),
    autoprefixer = require('autoprefixer'),
    webpack = require('webpack');

var prod = process.env.NODE_ENV === 'prod';
var action = process.env.WEBPACK_ACTION;

var commonConfig = {
    postcss: function () {
        return [precss, autoprefixer]
    },
    module: {
        loaders: [{
            test: /\.vue$/,
            loader: 'vue',
        }, {
            test: /(node_modules.*src.*|js).*\.js$/,
            loader: 'babel',
            query: {
                presets: ['es2015']
            }
        }, { 
            test: /\.css$/, 
            loader: "style/url!file" 
        }, {
            test: /\.json$/,
            loader: 'json'
        }, {
            test: /\.scss$/,
            loader: 'style!css!postcss!sass'
        }, { 
            test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, 
            loader: "url-loader?limit=10000&mimetype=application/font-woff" 
        }, { 
            test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, 
            loader: "file-loader" 
        }]
    },

    resolve: {
        root: [
            path.resolve('.'),
            path.resolve('./js'),
            path.resolve('./js/components')
        ]
    }
}

var config = {};

if (action === 'vendor')
     config = {
        entry: {
            vendor: 'js/vendor.js'
        },
        output: {
            publicPath: '/static/',
            path: path.join(__dirname, 'vendor_build'), 
            filename: "[name].js", 
        }
    }

else if (action === 'app')
    config = {
        devtool: prod ? '' : "source-map", 
        entry: {
            app: 'js/main'
        },
        output: {
            publicPath: '/static/',
            path: path.join(__dirname, prod ? 'build' : 'dest'), 
            filename: "[name].js", 
        }
    }

module.exports = Object.assign(commonConfig, config)

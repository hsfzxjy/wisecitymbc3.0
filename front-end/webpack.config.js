var path = require('path'),
    BundleTracker = require('webpack-bundle-tracker'),
    webpack = require('webpack');

module.exports = {
    devtool: "source-map",  
    entry: {
        app: 'js/main.es',
        vendor: [
            'jquery',
            'tether',
            'lodash',
            'bootstrap/dist/js/bootstrap.min.js',
            //'vendor/plupload.full.min.js',
            'bower_components/qiniu/dist/qiniu.min.js'
        ]
    },
    output: {
        publicPath: '/static/',
        path: path.join(__dirname, "dest/"), 
        filename: "[name].js", 
    },
    module: {
        loaders: [{
            test: /\.vue$/,
            loader: 'vue',
        }, {
            test: /(\.es)|(node_modules.*src.*\.js)$/,
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
            loader: 'style!css!sass'
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
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.ProvidePlugin({
            jQuery: "jquery",
            'window.Tether': 'tether',
            _: 'lodash'
        }),
        new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.bundle.js', Infinity)
    ]
};
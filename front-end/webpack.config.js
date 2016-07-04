var path = require('path'),
    BundleTracker = require('webpack-bundle-tracker'),
    webpack = require('webpack');

module.exports = {
    devtool: "source-map",  
    entry: {
        app: 'main.es',
        vendor: [
            'jquery',
            'tether',
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
        }]
    },

    resolve: {
        root: [
            path.resolve('.')
        ]
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.ProvidePlugin({
            jQuery: "jquery",
            'window.Tether': 'tether',
        }),
        new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.bundle.js', Infinity)
    ]
};
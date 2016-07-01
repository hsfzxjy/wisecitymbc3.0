var path = require('path'),
    BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    devtool: "source-map",  
    entry: './main.es',         
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
        new BundleTracker({filename: './webpack-stats.json'})
    ]
};
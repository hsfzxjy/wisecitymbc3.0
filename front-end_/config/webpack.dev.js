let base = require('./webpack.base')

module.exports = {
    entry: 'src/app',
    module: {
        loaders: base.loaders
    },
    resolve: base.resolve,
    output: {
        path: 'tmp/',
        filename: '[name].js'
    }
}
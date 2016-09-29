let path = require('path')

module.exports.loaders = [
    {
        test: /\.vue$/,
        loader: 'vue'
    },
    {
        test: /src.*\.js$/,
        loader: 'babel',
        query: {
            presets: ['es2015']
        }
    }
]

module.exports.resolve = {
    root: [
        path.resolve('.'),
        path.resolve('./js'),
        path.resolve('./js/components')
    ]
}
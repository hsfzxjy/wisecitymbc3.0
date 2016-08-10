import VueResource from 'vue-resource'

export default function (Vue) {
    Vue.use(VueResource)

    Vue.http.options.root = '/api'
    // Vue.http.headers.common['X-CSRFToken'] = /csrftoken=(.*)(\s|;|$)/.exec(document.cookie)[1]

    Vue.http.interceptors.push(function (request, next) {
        if (!_.isUndefined(this.loading)) {
            this.loading = true
            next(function (response) {
                this.loading = false
            })
        } else next()
    })

    Vue.http.interceptors.push(function (request, next) {
        if (!_.isUndefined(this.errors)) {
            next(function (response) {
                if (response.status === 400)
                    this.errors = response.data
            })
        } else next()
    })
}
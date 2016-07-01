import VueResource from 'vue-resource'

export default function (Vue) {
    Vue.use(VueResource)

    Vue.http.options.root = '/api'
    Vue.http.headers.common['X-CSRFToken'] = /csrftoken=(.*)(\s|;|$)/.exec(document.cookie)[1]
}
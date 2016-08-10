function timeSince(date) {

    var seconds = Math.floor((new Date() - date) / 1000);

    var interval = Math.floor(seconds / 31536000);

    if (interval > 1) {
        return interval + " 年";
    }
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) {
        return interval + " 月";
    }
    interval = Math.floor(seconds / 86400);
    if (interval > 1) {
        return interval + " 天";
    }
    interval = Math.floor(seconds / 3600);
    if (interval > 1) {
        return interval + " 小时";
    }
    interval = Math.floor(seconds / 60);
    if (interval > 1) {
        return interval + " 分钟";
    }
    return Math.floor(seconds) + " 秒";
}

export default function (Vue) {
    Vue.filter('state', (value) => _.isEmpty(value) ? '' : 'danger')
    Vue.filter('timesince', (value) => timeSince(new Date(value+'+08:00'))+'前')
    Vue.filter('br', value => value.replace(/[\r\n]+/g, '<br>'))
    Vue.filter('user', user => {
        return `<a href="#!${user.url}">${user.nickname}</a>`
    })
}
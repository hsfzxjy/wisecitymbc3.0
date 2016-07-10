import { StrUtils } from 'utils/index.es'

export default {
    route: {
        canActivate (transition) {
            return StrUtils.isDigits(transition.to.params.id)
        },
        data (transition) {
            let id = transition.to.params.id
            let config = this.$options.detailConfig
            let baseURL = config.baseURL

            return this.$http.get(`${baseURL}${id}/`)
                .then((res) => ({
                    [config.objectFieldName]: res.data,
                    [config.idFieldName]: id
                }))
        }
    }
}
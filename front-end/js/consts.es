export const AVAILABLE_CATEGORIES = ['government', 'company', 'media', 'finance', 'energy_and_raw_materials', 'electronic_technology', 'bank', 'real_estate']
export const CATEGORIES_NAME = ['政府', '公司', '媒体', '交易', '能源及原材料', '电子科技', '银行', '房地产']

import consts from 'consts.json'

export let articles = consts.articles
export let files = consts.files
export let accounts = consts.accounts

let UserType = consts.accounts.UserType

export let USER_TYPES = {
    [UserType.government]: '政府',
    [UserType.bureau]: '主席团',
    [UserType.company]: '选手'
}
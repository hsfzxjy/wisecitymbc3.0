export const AVAILABLE_CATEGORIES = ['government', 'company', 'media', 'finance', 'energy_and_raw_materials']

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
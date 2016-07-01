export const AVAILABLE_CATEGORIES = ['government', 'company', 'media']

import consts from 'consts.json'

let UserType = consts.accounts.UserType

export let USER_TYPES = {
    [UserType.government]: '政府',
    [UserType.bureau]: '主席团',
    [UserType.company]: '选手'
}
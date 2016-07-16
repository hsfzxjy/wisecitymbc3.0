<template>
    <div :class="class">
        <vs-nav 
            type="pills" :vertical="vertical">
            <vs-nav-item
                v-for="category in categories"
                :link="'/articles/'+$key+'/'"
                :active='$key === currentCategory'>
                {{ category }}
            </vs-nav-item>
        </vs-nav>
    </div>
</template>

<script>
    import { AVAILABLE_CATEGORIES, articles, CATEGORIES_NAME } from 'consts.es'

    export default {
        data: () => ({
            categories: _.zipObject(AVAILABLE_CATEGORIES, CATEGORIES_NAME),
        }),
        props: {
            vertical: {
                type: Boolean,
                default: false
            },
            class: {
                default: ''
            },
            currentCategory: {
                type: [String, Number],
                default: 'none',
                coerce (value) {
                    if (_.isNumber(value)) {
                        let key

                        _.forEach(articles.ArticleType, (v, k) => {
                            if (v === value) key = k
                        })

                        return key
                    }

                    return value
                }
            }
        },
    }
</script>
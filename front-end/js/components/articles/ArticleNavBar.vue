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
    export default {
        data: () => ({
            categories: consts.article_type_verbose,
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

                        _.forEach(consts.ArticleType, (v, k) => {
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
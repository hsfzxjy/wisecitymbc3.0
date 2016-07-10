<template>
    <form>
        <slot></slot>
    </form>
</template>

<script>

    function getName (el) {
        let attr = _.find(el.attributes, { name: 'name' }) || null
        return attr ? attr.value : null;
    }

    export default {
        props: {
            errors: {
                type: Object,
                default: {}
            }
        },
        watch: {
            errors: {
                deep: true,
                handler (value, oldValue) {
                    this.setErrors()
                }
            }
        },
        methods: {
            setErrors () {
                console.log(this)
                _.forEach(this.$el, $child => {
                    let name = getName($child)
                    if (!name || !$child.__vue__) return
                    $child.__vue__.state = this.$interpolate(`{{ errors.${name} | state }}`)
                })
            }
        }
    }
</script>
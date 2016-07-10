<template>
    <fieldset class="form-group {{inputState}}">
        <div class="inputClass">
            <button 
                type="{{type}}" 
                class="btn {{btnVariant}} {{btnSize}} {{btnBlock}} {{inactive ? 'btn-inactive' : ''}} {{btnDisabled}}">
                <slot></slot>
            </button>
        </div>
    </fieldset>
</template>

<script>
    export default {
      replace: true,
      computed: {
        btnBlock() {
          return this.block ? `btn-block` : ``
        },
        btnVariant() {
          return !this.variant || this.variant === `default` ? `btn-secondary` : `btn-${this.variant}`
        },
        btnSize() {
          return !this.size || this.size === `default` ? `` : `btn-${this.size}`
        },
        btnDisabled() {
          return this.disabled ? 'disabled' : ''
        },
        inputSize() {
          return !this.size || this.size === `default` ? `` : `form-control-${this.size}`
        },
      },
      props: {
        block: {
            type: Boolean,
          default: false
        },
        disabled: {
          type: Boolean,
          default: false
        },
        inactive: {
            type: Boolean,
          default: false
        },
        link: {
            type: String,
          default: ''
        },
        role: {
            type: String,
          default: ''
        },
        size: {
          type: String,
          default: 'md'
        },
        type: {
            type: String,
            default: 'submit'
        },
        variant: {
          type: String,
          default: 'default'
        },
      },
    }
</script>
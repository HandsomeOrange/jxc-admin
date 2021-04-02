<script type="text/jsx">
import {deepClone} from "@/util"
import {getElementInnerWidth} from '@/util/browser'
import {clearableComponentTag, clearFormItem} from "@/util/element-ui/elForm"
import {findComponentByTag} from "@/util/vue"

export default {
  name: "SearchForm",

  model: {
    prop: 'model',
    event: 'reset'
  },

  props: {
    model: Object,
    labelWidth: {type: String, default: '120px'},

    /*每个宽度下，一行能有多少个控件，需要是24的因数*/
    xs: {type: Number, default: 1}, // <768px
    sm: {type: Number, default: 2}, // >=768px
    md: {type: Number, default: 3}, // >=998px
    lg: {type: Number, default: 4},  // >=1200px
  },

  data() {
    return {
      showCollapse: false, //是否需要折叠控制
      collapse: true,      //是否处于折叠状态，默认折叠
      num: 0,              //从第几个控件开始需要隐藏
      span: 8,           //24等分下，每个栅格的宽度
    }
  },

  methods: {
    handleCollapse() {
      this.collapse = !this.collapse
    },
    handleSearch() {
      this.$emit('search')
    },
    handleReset() {
      if (!this.initialModel || !this.model) {
        return
      }

      this.$slots.default.forEach(({componentInstance}) => {
        const item = findComponentByTag(componentInstance, tag => clearableComponentTag.includes(tag))
        item && clearFormItem(item)
      })

      //因为表单可能存在无清空功能的组件，所以传递一次初始值
      this.$emit('reset', deepClone(this.initialModel))
      this.$emit('search')
    },

    getElementNumInRow() {
      const vw = getElementInnerWidth(this.$el.parentNode)

      if (vw < 768) return this.xs
      if (vw < 998) return this.sm
      if (vw < 1200) return this.md
      return this.lg
    },

    resize() {
      const num = this.getElementNumInRow()

      this.span = 24 / num

      //考虑后面的按钮组的占位
      this.num = num === 1 ? num : num - 1

      this.showCollapse = this.num < this.$slots.default.length
    },

    renderChildren(children, hide) {
      return children.map(child => (
          <el-col span={this.span} class={{hide}}>{child}</el-col>
      ))
    },

    renderAction() {
      const ctrl = this.collapse
          ? {i: 'el-icon-arrow-down', t: '展开'}
          : {i: 'el-icon-arrow-up', t: '收起'}
      // console.log('this.showCollectButton()==' + this.showCollectButton())
      // console.log(this.showCollectButton)
      return (
          <div class="search-form-action">
                <el-button type="success" icon="el-icon-sold-out" id="collect" size="small"
                           on-click={this.handleSearch}>采
                  集
                </el-button>
            <el-button type="primary" icon="el-icon-refresh" size="small" on-click={this.handleReset}>刷
              新
            </el-button>
          </div>
      )
    }
  },

  mounted() {
    //记录初始条件
    this.initialModel = deepClone(this.model)

    this.resize()
    this.resizeObserver = new ResizeObserver(this.resize)
    this.resizeObserver.observe(this.$el.parentNode)

    this.$once('hook:beforeDestroy', () => {
      if (this.resizeObserver) {
        this.resizeObserver.disconnect()
        this.resizeObserver = null
      }
    })
  },

  render() {
    const slots = this.$slots.default, collapse = this.showCollapse && this.collapse
    const display = collapse ? slots.slice(0, this.num) : slots
    const hidden = collapse ? slots.slice(this.num) : []
    return (
        <el-form
            class="search-form"
            label-position="right"
            label-width={this.labelWidth}
            label-suffix=":"
            size="small"
        >
          <el-row gutter={20}>
            {this.renderChildren(display)}
            {this.renderChildren(hidden, true)}
            {this.renderAction()}
          </el-row>
        </el-form>
    )
  }
}
</script>

<style lang="scss">
.search-form {
  &-action {
    margin-left: auto;
  }

  > .el-row {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }

  .el-col.hide {
    display: none;
  }
}
</style>

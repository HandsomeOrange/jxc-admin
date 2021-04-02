export default {
    path: 'cool',
    meta: {title: 'Shopify导出', icon: 'el-icon-s-opportunity'},
    children: [
        {
            path: 'fluid',
            component: 'example/cool/fluid',
            meta: {title: '单链接采集'}
        },
        {
            path: 'l2d',
            component: 'example/cool/l2d',
            meta: {title: '多链接采集'}
        },
        {
            path: 'collection',
            component: 'example/cool/collection',
            meta: {title: '按类别采集'}
        },
    ]
}

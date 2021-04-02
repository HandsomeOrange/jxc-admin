export default {
    path: '/shopify',
    meta: {title: 'Shopify导出', icon: 'el-icon-sold-out', noAuth: true, noCache: true, sort: 2},
    component: 'Layout',
    children: [
        {
            path: 'link',
            component: 'shopify/link',
            meta: {title: '按链接采集'}
        },
        {
            path: 'collection',
            component: 'shopify/collection',
            meta: {title: '按类别采集'}
        },
    ]
}

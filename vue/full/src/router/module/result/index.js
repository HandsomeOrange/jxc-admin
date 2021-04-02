export default {
    path: '/result',
    meta: {title: '全部导出', icon: 'el-icon-sold-out', noAuth: true, noCache: true, sort: 99},
    component: 'Layout',
    children: [
        {
            path: 'list',
            component: 'result/',
            meta: {title: '全部导出',icon: 'el-icon-s-data'}
        }
    ]
}

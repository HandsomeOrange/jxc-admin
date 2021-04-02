import {GetApi, PostApi} from "@/api/request"

export const getById = new GetApi('/doc/sell/order/getById', id => ({params: {id}}))

export const getSubById = new GetApi('/doc/sell/order/getSubById', id => ({params: {id}}))

export const search = new PostApi('/shopify/submit')

export const exportExcel = new PostApi('/doc/sell/order/export')

export const add = new PostApi('xx')

export const update = new PostApi('/doc/sell/order/update')

export const commit = new PostApi('/doc/sell/order/commit')

export const withdraw = new PostApi('/doc/sell/order/withdraw')

export const pass = new PostApi('/doc/sell/order/pass')

export const reject = new PostApi('/doc/sell/order/reject')

export const del = new GetApi('/shopify/del', id => ({params: {id}}))
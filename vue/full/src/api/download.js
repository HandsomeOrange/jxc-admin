import {GetApi, PostApi} from "@/api/request"

export const downloadById = new GetApi('/download/by-id', id => ({params: {id}}))
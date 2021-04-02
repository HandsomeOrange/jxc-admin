<template>
  <list-page :data="listPageConfig">
<!--    <template v-slot:searchForm>-->
<!--      <el-form-item label="Shopify产品类别链接" label-width="160px"  v-show="false">-->
<!--        <el-input placeholder="example:http://www.xxxx.com/collections/bag" v-model="searchForm.collectionUrl"-->
<!--                  clearable/>-->
<!--      </el-form-item>-->
<!--      <div style="display: none" v-bind:showCollectButton="!isResultPage"></div>-->
<!--    </template>-->
    <template v-slot:tableColumn>
      <el-table-column align="center" label="序号" type="index" width="80"/>
      <el-table-column align="center" label="采集链接" prop="linkUrl" show-overflow-tooltip/>
      <el-table-column align="center" label="采集站点" prop="fromSite" width="150"/>
      <el-table-column align="center" label="采集类型" prop="productExport" width="150" :formatter="formatExportType"/>
      <el-table-column align="center" label="采集商品数" prop="productNumber" width="150"/>
      <el-table-column align="center" label="采集时间" prop="exportTime" width="150"/>
      <el-table-column align="center" label="耗 时" prop="duration" width="100" :formatter="formatDuration"/>
      <el-table-column align="center" label="状 态" width="120">
        <template v-slot="{row}">
          <span :class="{primary:row.status===0,success:row.status===1,danger:row.status===-1}" class="dot"/>
          {{ getStatus(row.status) }}
        </template>
      </el-table-column>
      <!--      <el-table-column align="center" label="导出文件" prop="exportFile" width="400"/>-->
      <el-table-column align="center" label="操作" width="200">
        <template v-slot="{row}">
          <el-row>
            <el-button type="primary" size="small" icon="el-icon-download" v-show="row.status===1"
                       v-on:click="download_(row.id, row.exportFile)">下载
            </el-button>
            <!--            <p>这是一段内容这是一段内容确定删除吗？</p>-->
            <!--            <div style="text-align: right; margin: 0">-->
            <!--              <el-button size="mini" type="text" @click="visible = false">取消</el-button>-->
            <!--              <el-button type="primary" size="mini" @click="visible = false">确定</el-button>-->
            <!--            </div>-->
            <el-button type="danger" size="small" icon="el-icon-delete" @click="del_(row.id)">删除</el-button>
          </el-row>
        </template>
      </el-table-column>


      <!--            <el-table-column align="center" label="完成时间" width="150">-->
      <!--                <template v-slot="{row}">{{ row.ftime | timestamp2Date }}</template>-->
      <!--            </el-table-column>-->
    </template>
  </list-page>
</template>

<script>
import docTableMixin from '@/mixin/docTableMixin'
import {add, update, del, withdraw, pass, reject, getSubById, search, exportExcel} from "@/api/doc/sell/shopify"
import {downloadById} from "@/api/download"
import {elConfirm, elSuccess} from "../../util/message";

export default {
  name: "shopify",

  mixins: [docTableMixin],

  data() {
    this.api = {add, update, del, withdraw, pass, reject, getSubById, search, exportExcel, downloadById}
    return {
      isResultPage: true,
      searchForm: {
        customerName: null,
        collectionUrl: null,
        fromSite: "shopify",
        maxProductSize: null,
        productExport: null
      },
      temp: {
        finish: [],
        ftime: []
      },
      excel: {
        columns: [
          {header: '序号', prop: 'id'},
          {header: 'xxxx', prop: 'customerName', width: 30},
          {header: '创建人', prop: 'cname'},
          {header: '创建时间', prop: 'ctime'},
          {header: '审核人', prop: 'vname'},
          {header: '审核时间', prop: 'vtime'},
          {header: '状态', prop: 'status'},
          {header: '完成情况', prop: 'finish'},
          {header: '完成时间', prop: 'ftime'},
          {header: '备注', prop: 'remark', width: 50}
        ]
      },
      buttons: []
    }
  },

  methods: {
    resultPage2() {
      return true
    },
    mergeSearchForm() {
      return {
        ...this.searchForm,
      }
    },
    download_(id, fileName) {
      this.api.downloadById
          .request(id).then(response => {
        // console.log('download res :' + response)
        const dataBlob = new Blob([`\ufeff${response}`], {type: 'text/plain;charset=utf-8'});//返回的格式
        // return window.URL.createObjectURL(dataBlob);
        const url = window.URL.createObjectURL(dataBlob);//{}指的是表头，res.data.data.workhour_csv_data是后台返回来的数据
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
      }).catch(error => {
        console.log(error)
      })
    },
    del_(id) {
      return elConfirm(`确定删除该导出记录？`)
          .then(() => {
            // this.config.operating = true
            return del.request(id)
          })
          .then(() => {
            elSuccess('删除成功')
            this.search()
          })
          .finally(() => this.config.operating = false)
    },
    formatDuration(row, column) {
      if (row[column.property]) {
        return row[column.property] + 's';
      }
      return '0s';
    },
    formatExportType(row, column) {
      return row[column.property] === 1 ? '商品链接采集' : '类别采集';
    },
  }
}


</script>
<!--<style>-->
<!--.el-col-6 {-->
<!--  width: 60%;-->
<!--}-->

<!--.search-form-action {-->
<!--  margin-left: 2%;-->
<!--  width: 60%;-->
<!--}-->

<!--.el-button&#45;&#45;dashed {-->
<!--  display: none;-->
<!--}-->

<!--.disable-button {-->
<!--  display: none;-->
<!--}-->

<!--</style>-->
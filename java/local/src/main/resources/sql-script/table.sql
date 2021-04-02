DROP TABLE IF EXISTS `export_history`;
CREATE TABLE `export_history`  (
                                   `id` varchar(50) NOT NULL COMMENT '主键id',
                                   `link` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '采集链接',
                                   `status` int(11) NOT NULL COMMENT '采集结果，0采集中，1采集成功，-1采集失败',
                                   `export_file` varchar(50) COMMENT '采集结果文件',
                                   `from_site` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '来自站点',
                                   `export_time` varchar(50) NOT NULL COMMENT '采集时间',
                                   PRIMARY KEY (`id`) USING BTREE
                                       #   INDEX `pid_time_idx`(`pid`, `time`) USING BTREE,
                                   #   INDEX `uid_idx`(`uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 70 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
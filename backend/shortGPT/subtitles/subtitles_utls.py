import re

PUNCTUATION_LIST = [",", "，", "。", ".", ";", "；", "!", "！", "?", "？"]
PUNCTUATION_pattern = r"([,，.。;；!！?？])"

def split_sentences(text):
    # 使用正则表达式将文本分割成句子
    sentences = re.split(PUNCTUATION_pattern, text)
    sentences = ["".join(pair) for pair in zip(sentences[0::2], sentences[1::2])]
    return sentences

def add_punctuation_to_srt(original_srt, subtitle_text):
    sentences = split_sentences(subtitle_text)

    # 将原有的SRT文件内容按行分割
    original_srt_list = original_srt.split("\n")

    def add_punctuation(list1, list2):
        # list1 = ['1', '00:00:00,100 --> 00:00:04,312', '当 生活 让 你 感到 疲惫不堪 时 不妨 停下脚步 放松', '', '2', '00:00:04,312 --> 00:00:07,800', '心情 看看 周围 的 美好 或许 是 一 只 小鸟', '', '3', '00:00:07,825 --> 00:00:10,250', '在 树枝 上 欢快 地 歌唱 或许 是 一 朵', '', '4', '00:00:10,275 --> 00:00:13,525', '娇艳 的 鲜花 在 微风 中 轻轻 摇曳 或许 是', '', '5', '00:00:13,537 --> 00:00:15,688', '一 杯 清香 的 茶 在 你 的 唇齿 间', '', '6', '00:00:15,713 --> 00:00:19,137', '缓缓 流淌 生活 中 有 太 多 美好 的 瞬间', '', '7', '00:00:19,250 --> 00:00:22,450', '值得 我们 去 发现 和 珍惜 让 这些 美好 温暖', '', '8', '00:00:22,462 --> 00:00:24,625', '你 的 心灵 让 你 的 内心 充满 爱 和', '', '9', '00:00:24,637 --> 00:00:28,400', '希望 你 会 发现 自己 变得 更加 强大 和 坚定', '', '']
        # list2 = ['当生活让你感到疲惫不堪时，', '不妨停下脚步，', '放松心情，', '看看周围的美好。', '或许是一只小鸟在树枝上欢快地歌唱，', '或许是一朵娇艳的鲜花在微风中轻轻摇曳，', '或许是一杯清香的茶在你的唇齿间缓缓流淌。', '生活中有太多美好的瞬间值得我们去发现和珍惜。', '让这些美好温暖你的心灵，', '让你的内心充满爱和希望，', '你会发现自己变得更加强大和坚定。']
        # 初始化索引和结果列表
        result = []
        list2_index = 0

        for line in list1:
            if any([not line, line.isdigit(), "-->" in line]):
                result.append(line if not line else line)
                continue

            new_line = line.split()
            
            for i in new_line:
                index = list2[list2_index].find(i)
                if index > -1 and list2[list2_index][index+len(i)] in PUNCTUATION_LIST:
                    new_line[new_line.index(i)] = i + list2[list2_index][index+len(i)] + " " # 找到了
                    list2_index += 1 # 从后面找
            result.append("".join(new_line))
    
        if result and result[-1] == "\n":
            result.pop(-1)

        return result

    return "\n".join(add_punctuation(original_srt_list, sentences))

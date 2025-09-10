#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说分割脚本
将大型小说文件按指定字数分割成多个小文件
"""

import os
import re


def split_novel(input_file, output_dir, words_per_file=100000):
    """
    分割小说文件
    
    Args:
        input_file: 输入的小说文件路径
        output_dir: 输出目录
        words_per_file: 每个文件的字数限制（默认10万字）
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取原始小说文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except UnicodeDecodeError:
        # 如果UTF-8失败，尝试GBK编码
        with open(input_file, 'r', encoding='gbk') as f:
            original_content = f.read()
    
    print(f"原文总字数: {len(original_content)}")
    
    # 计算需要分割的文件数量
    total_files = (len(original_content) + words_per_file - 1) // words_per_file
    print(f"预计分割成 {total_files} 个文件")
    
    # 记录实际的分割位置
    split_positions = [0]  # 起始位置
    current_pos = 0
    
    # 先计算所有分割位置
    for i in range(total_files - 1):  # 最后一个文件不需要计算分割点
        target_pos = current_pos + words_per_file
        
        # 如果超出文件长度，直接结束
        if target_pos >= len(original_content):
            break
            
        # 寻找合适的断句点
        best_pos = target_pos
        for j in range(min(target_pos, len(original_content) - 1), 
                      max(current_pos + words_per_file - 1000, current_pos), -1):
            if j < len(original_content) and original_content[j] in '。！？':
                best_pos = j + 1
                break
        
        split_positions.append(best_pos)
        current_pos = best_pos
    
    # 添加文件结尾位置
    split_positions.append(len(original_content))
    
    # 根据分割位置生成文件
    actual_files = len(split_positions) - 1
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    
    for i in range(actual_files):
        start_pos = split_positions[i]
        end_pos = split_positions[i + 1]
        
        # 获取当前分片内容
        chunk = original_content[start_pos:end_pos]
        
        # 跳过空内容
        if len(chunk.strip()) == 0:
            continue
            
        # 生成输出文件名
        output_file = os.path.join(output_dir, f"{base_filename}_{i+1:03d}.txt")
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        
        print(f"已生成: {output_file} (字数: {len(chunk)})")
    
    print(f"分割完成！共生成 {actual_files} 个文件")


def find_first_txt_file(directory):
    """
    在指定目录中查找第一个txt文件
    
    Args:
        directory: 要搜索的目录路径
        
    Returns:
        找到的第一个txt文件路径，如果没找到返回None
    """
    if not os.path.exists(directory):
        return None
    
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith('.txt'):
            return os.path.join(directory, filename)
    
    return None


def main():
    """主函数"""
    # 配置参数
    xs_dir = "xs"
    words_per_file = 100000  # 每个文件的字数（10万字）
    
    # 自动查找第一个txt文件
    input_file = find_first_txt_file(xs_dir)
    if not input_file:
        print(f"错误：在 {xs_dir} 目录中没有找到任何txt文件")
        print("请确保在 xs 目录中放入小说文件")
        return
    
    # 获取文件名（不含扩展名）作为输出目录名
    filename = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(xs_dir, f"{filename}_chapters")
    
    print(f"找到小说文件: {input_file}")
    print(f"输出目录: {output_dir}")
    
    print(f"每个分片大小: {words_per_file:,} 字")
    print("-" * 50)
    
    # 执行分割
    split_novel(input_file, output_dir, words_per_file)


if __name__ == "__main__":
    main()
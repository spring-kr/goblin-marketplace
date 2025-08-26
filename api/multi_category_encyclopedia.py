#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
분할된 백과사전 통합 시스템
"""

import logging

logger = logging.getLogger(__name__)

def load_all_categories():
    """모든 카테고리 데이터 로드"""
    categories = {}
    category_modules = [
        ('business', 'encyclopedia_business', 'BUSINESS_DATA'),
        # ('technology', 'encyclopedia_technology', 'TECHNOLOGY_DATA'),
        # ('psychology', 'encyclopedia_psychology', 'PSYCHOLOGY_DATA'),
        # ('science', 'encyclopedia_science', 'SCIENCE_DATA'),
        # ('society', 'encyclopedia_society', 'SOCIETY_DATA')
    ]
    
    for category_name, module_name, data_var in category_modules:
        try:
            module = __import__(module_name)
            data = getattr(module, data_var)
            categories[category_name] = data
            logger.info(f"카테고리 '{category_name}' 로드 완료: {len(data.get('articles', {}))}개 기사")
        except Exception as e:
            logger.error(f"카테고리 '{category_name}' 로드 실패: {e}")
    
    return categories

def get_multi_category_answer(query):
    """여러 카테고리에서 답변을 검색합니다"""
    
    # 모든 카테고리 데이터 로드
    all_data = load_all_categories()
    
    # 1. 의미적 매칭 먼저 시도 (고객중심 -> 고객 관련)
    semantic_result = search_semantic_match(query, all_data)
    if semantic_result:
        return semantic_result
    
    # 2. 직접 키워드 검색
    direct_result = search_direct_keywords(query, all_data)
    if direct_result:
        return direct_result
    
    # 3. 부분 매칭 검색
    partial_result = search_partial_keywords(query, all_data)
    if partial_result:
        return partial_result
    
    # 4. 내용 검색
    content_result = search_content(query, all_data)
    if content_result:
        return content_result
        
    return f"'{query}'에 대한 정보를 찾을 수 없습니다."

def search_semantic_match(query, all_data):
    """의미적으로 연관된 키워드 검색"""
    # 고객중심, 고객지향 등을 고객으로 매핑
    semantic_mappings = {
        '고객중심': ['고객', '마케팅', '서비스'],
        '고객지향': ['고객', '마케팅', '서비스'],
        '고객서비스': ['고객', '서비스', '마케팅'],
        '고객만족': ['고객', '서비스', '마케팅'],
        '소비자중심': ['고객', '소비자', '마케팅'],
        '시장지향': ['시장', '마케팅', '경제'],
    }
    
    # 쿼리에 매핑된 키워드가 있는지 확인
    for semantic_key, related_terms in semantic_mappings.items():
        if semantic_key in query or any(term in query for term in related_terms):
            # 관련 키워드로 검색
            for term in related_terms:
                for category_name, data in all_data.items():
                    # 키워드에서 검색
                    for keyword, article_ids in data['keywords'].items():
                        if term in keyword:
                            best_article = find_best_article(article_ids, data['articles'], query)
                            if best_article:
                                return format_answer(best_article, keyword, category_name)
                    
                    # 기사 제목에서 검색
                    for article_id, article in data['articles'].items():
                        if term in article['title']:
                            return format_answer(article, f"제목: {article['title']}", category_name)
    
    return None

def search_direct_keywords(query, all_data):
    """직접 키워드 매칭"""
    for category_name, data in all_data.items():
        for keyword, article_ids in data['keywords'].items():
            if query.lower() in keyword.lower() or keyword.lower() in query.lower():
                best_article = find_best_article(article_ids, data['articles'], query)
                if best_article:
                    return format_answer(best_article, keyword, category_name)
    return None

def search_partial_keywords(query, all_data):
    """부분 매칭 검색"""
    query_words = query.lower().split()
    for category_name, data in all_data.items():
        for keyword, article_ids in data['keywords'].items():
            keyword_words = keyword.lower().split()
            if any(q_word in keyword.lower() for q_word in query_words) or \
               any(k_word in query.lower() for k_word in keyword_words):
                best_article = find_best_article(article_ids, data['articles'], query)
                if best_article:
                    return format_answer(best_article, keyword, category_name)
    return None

def search_content(query, all_data):
    """내용 검색"""
    for category_name, data in all_data.items():
        for article_id, article in data['articles'].items():
            if query.lower() in article['content'].lower() or query.lower() in article['title'].lower():
                return format_answer(article, f"내용 검색: {query}", category_name)
    return None

def find_best_article(article_ids, articles, query):
    """가장 적합한 기사 찾기"""
    if not article_ids:
        return None
    
    # 첫 번째 기사 반환 (개선 가능)
    first_id = article_ids[0] if isinstance(article_ids, list) else article_ids
    return articles.get(first_id)

def format_answer(article, matched_keyword, category):
    """답변 포맷팅"""
    return f"""**{article['title']}** (출처: {category})

**요약:** {article['summary']}

**상세 내용:**
{article['content'][:500]}...

*매칭된 키워드: {matched_keyword}*"""

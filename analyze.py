from elasticsearch_dsl import analyzer,analysis

lowercase_english = analysis.token_filter('english_lowercase', type="lowercase")


stopword_english = analysis.token_filter('english_stopword', type='stop', stopwords='_english_')


tokenizer_english = analysis.tokenizer('punctuation', type='pattern', pattern="[-1234567890,.!'~#@*+%{}<>\\[\\]|\"_^]")


bigram_filter = analysis.token_filter('edge_ngram_filter', type="edge_ngram",
                                      min_gram=3, max_gram=3, )


stemming_filter = analysis.token_filter('stemming_filter', type='snowball')


custom_filtering = analyzer('custom_filtering',
                            type="custom",
                            tokenizer=tokenizer_english,
                            filter=[lowercase_english, stopword_english, bigram_filter, stemming_filter],

                            )

from nlp_sim.svm import svm


if __name__ == '__main__':
    paths = dict()
    prefix = 'nlp_sim/'
    paths['data_clean'] = prefix + 'data/train_clean.csv'
    paths['label'] = prefix + 'data/train_label.txt'
    paths['bow_feat'] = prefix + 'feat/svm/bow_train.pkl'
    paths['tfidf_feat'] = prefix + 'feat/svm/tfidf_train.pkl'
    paths['svm_line_bow'] = prefix + 'model/svm/line_bow.pkl'
    paths['svm_line_tfidf'] = prefix + 'model/svm/line_tfidf.pkl'
    paths['svm_rbf_bow'] = prefix + 'model/svm/rbf_bow.pkl'
    paths['svm_rbf_tfidf'] = prefix + 'model/svm/rbf_tfidf.pkl'
    svm(paths, 'line', 'bow', 'train')
    svm(paths, 'line', 'tfidf', 'train')
    svm(paths, 'rbf', 'bow', 'train')
    svm(paths, 'rbf', 'tfidf', 'train')
    paths['data_clean'] = prefix + 'data/dev_clean.csv'
    paths['label'] = prefix + 'data/dev_label.txt'
    paths['bow_feat'] = prefix + 'feat/svm/bow_dev.pkl'
    paths['tfidf_feat'] = prefix + 'feat/svm/tfidf_dev.pkl'
    svm(paths, 'line', 'bow', 'dev')
    svm(paths, 'line', 'tfidf', 'dev')
    svm(paths, 'rbf', 'bow', 'dev')
    svm(paths, 'rbf', 'tfidf', 'dev')

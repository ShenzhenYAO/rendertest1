# copied from C:\Personal\Virtual_Server\PHPWeb\lit_d3python\python\tools\refined_tools.py
# refined tools from tools_py and other script files
# modified by saving confusion matrix png files instead of showing them
def classify_multi_methods(clf_dict, testsize=0.5, targetpath='' , file_prefix='cm_', models='', make_cm_pngs = 1, multinomialnb = 1):
########################################################

    # 1. use train_test_split to split the training and test sets
    print ('    making train and test sets...')
    # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    # the input set should be like x and y, x can be a list like [[...], [...]], y [[..],[..]]
    # the following is to randomly split the data into half for training, half test
    # the order is like trainx, testx, trainy, testy
    # the random_state is like a random seed, to control that each time the randomization produces the same results
    # hey, the train and test set can be split by the kit!
    from sklearn.model_selection import train_test_split
    x = clf_dict['x']
    y = clf_dict['y']
    trainx_ls, testx_ls, trainy_ls, testy_ls = train_test_split(
    x, y, test_size=testsize, random_state=42)


    # 2. bulding classification methods
    print ('    building classification methods...')
    # https://github.com/amkurian/gender_classification/blob/master/gender_classifier.py 
    #######################################################
    # print ('testsize = ' + str(testsize))
    import numpy as np
    from sklearn.naive_bayes import GaussianNB
    from sklearn.naive_bayes import BernoulliNB
    from sklearn.naive_bayes import MultinomialNB
    from sklearn import tree
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression
    from sklearn import neighbors
    from sklearn.neural_network import MLPClassifier

    #Create a Gaussian Classifier (naive bayesian)
    print ('        Gaussian (naive bayesian) Classifier...')
    nb_clf = GaussianNB()
    # Train the model using the training sets
    nb_clf=nb_clf.fit(trainx_ls,trainy_ls)
    nb_prediction =nb_clf.predict(testx_ls)
    # print (nb_prediction)

    print ('        BernoulliNB Classifier...')
    #Create a BernoulliNB Classifier (naive bayisian)
    bl_clf = BernoulliNB()
    # Train the model using the training sets
    bl_clf=bl_clf.fit(trainx_ls,trainy_ls)
    bl_prediction =bl_clf.predict(testx_ls)
    #print (bl_prediction)

    if multinomialnb == 1:
        print ('        MultinomialNB Classifier...')
        #Create a MultinomialNB Classifier (naive bayisian)
        mb_clf = MultinomialNB()
        # Train the model using the training sets
        mb_clf=mb_clf.fit(trainx_ls,trainy_ls)
        mb_prediction =mb_clf.predict(testx_ls)
        #print (mb_prediction)

    #DecisionTreeClassifier
    print ('        DecisionTree Classifier...')
    dtc_clf = tree.DecisionTreeClassifier()
    dtc_clf = dtc_clf.fit(trainx_ls,trainy_ls)
    dtc_prediction = dtc_clf.predict(testx_ls)

    #RandomForestClassifier
    print ('        RandomForest Classifier...')
    rfc_clf = RandomForestClassifier()
    rfc_clf.fit(trainx_ls,trainy_ls)
    rfc_prediction = rfc_clf.predict(testx_ls)

    #Supporting Vector Machines Classifier
    print ('        Supporting vector machines (SVM/SVC) Classifier...')
    s_clf = SVC()
    s_clf.fit(trainx_ls,trainy_ls)
    s_prediction = s_clf.predict(testx_ls)

    #LogisticRegression
    print ('        Logistic regression Classifier...')
    l_clf = LogisticRegression()
    l_clf.fit(trainx_ls,trainy_ls)
    l_prediction = l_clf.predict(testx_ls)

    #NearestNeighbors
    print ('        K-Nearest Neighbors (KNN) Classifier...')
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=5)
    knn_clf.fit(trainx_ls,trainy_ls)
    knn_prediction = knn_clf.predict(testx_ls)

    # Multi-layer Perceptron (MLP)
    print ('        Multi-layer Perceptro(MLP) Classifier...')
    # https://www.kaggle.com/ahmethamzaemra/mlpclassifier-example
    # mp_clf = MLPClassifier(hidden_layer_sizes=(100,100,100), max_iter=500, alpha=0.0001,
    #                      solver='sgd', verbose=10,  random_state=21,tol=0.000000001)
    # 0.9735772357723578
    # https://analyticsindiamag.com/a-beginners-guide-to-scikit-learns-mlpclassifier/
    mp_clf = MLPClassifier(hidden_layer_sizes=(150,100,50), max_iter=500,activation = 'relu',solver='adam',random_state=1)
    # 0.9744483159117305
    mp_clf.fit(trainx_ls,trainy_ls)
    mp_prediction = mp_clf.predict(testx_ls)

    def not_run_tf(): # tf model is kicked out as it is useless
        #### the following part is specifically for tensorflow clf #############
        print ('        Tensorflow(ts) Classifier...')
        # 1. make a dictionary of y values, i.e., {'adh', 'both', 'doc', 'none'}
        yvalues_dict=set(y)
        # 2. make a dict for y values, like ['none':0, 'adh':1...]
        idxy_dict = {x:i for i,x in enumerate(yvalues_dict)}  
        # 3. convert y values from strings to index numbers
        y_idx = [idxy_dict[x] for x in y if x in idxy_dict] 
        trainyidx_ls= [idxy_dict[x] for x in trainy_ls if x in idxy_dict] 
        testyidx_ls= [idxy_dict[x] for x in testy_ls if x in idxy_dict] 

        # # use sklearning kit's split method to make training and test ls
        # from sklearn.model_selection import train_test_split
        # trainx_ls, testx_ls, trainyidx_ls, testyidx_ls = train_test_split(
        # x, y_idx, test_size=testsize, random_state=42)

        # $ pip install tensorflow -- user
        import tensorflow as tf

        # https://www.tensorflow.org/tutorials/keras/classification
        # 1. define the model and specify layers
        n_yvalues=len(yvalues_dict)
        model = tf.keras.Sequential([
            ## if the x is already flatterned (as in this example), no need to run the following line
            # tf.keras.layers.Flatten(input_shape=(25, 1)),
            tf.keras.layers.Dense(10000, activation='relu'), #used to be 128
            tf.keras.layers.Dense(n_yvalues) # this must be conform with the length of the y values
        ])
        ## do not use the following if .Flatten is not properly specified
        # model.output_shape
        # 2. compile the model (more specifications...)
        model.compile(optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
        # 3. fit the model, like building a classification algorithm
        # epoch stands for number fo times to repeat/try
        model.fit(trainx_ls, trainyidx_ls, epochs=10)
        # 4. apply the algorithm to test data and evaluate accuracy
        test_loss, test_acc = model.evaluate(testx_ls,  testyidx_ls, verbose=2)
        # 5. if the accuracy is good (like > .90), use the algorithm to make predictions
        probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
        ts_prediction_prob = probability_model.predict(testx_ls)
        # 6. For each observation, select the index of the max probabilities (see example clf_ts_sentence.py for explanationon the one line code)
        ts_prediction_yidx_ls = list(map(lambda yt:[i for i,x in enumerate(yt) if x == max(yt)][0] , ts_prediction_prob))
        # 7. translate the predictied index to y values
        ts_prediction_y_ls = list (map(lambda yidx: list(idxy_dict.keys())[list(idxy_dict.values()).index(yidx)], ts_prediction_yidx_ls))

        ts_prediction = ts_prediction_y_ls
        ts_clf=probability_model
        # no need to calculate testy_ts_ls, it is the same as testy_ls with has been prepared
        # testy_ts_ls = list (map(lambda yidx: list(idxy_dict.keys())[list(idxy_dict.values()).index(yidx)], testyidx_ls))
        #### the above part is specifically for tensorflow clf #############

    # 3. calculate accuracy
    print ('    Calculating accuracy of each classifier...')
    from sklearn.metrics import accuracy_score
    #######################################################
    #accuracy scores
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html
    # accuracy_score(true or observed, predicted)
    nb_acc = accuracy_score(testy_ls, nb_prediction)
    bl_acc = accuracy_score(testy_ls, bl_prediction)
    if multinomialnb == 1:
        mb_acc = accuracy_score(testy_ls, mb_prediction)
    dtc_tree_acc = accuracy_score(testy_ls, dtc_prediction)
    rfc_acc = accuracy_score(testy_ls, rfc_prediction)
    l_acc = accuracy_score(testy_ls, l_prediction)
    s_acc = accuracy_score(testy_ls,s_prediction)
    knn_acc = accuracy_score(testy_ls, knn_prediction)
    # mp_acc= accuracy_score(testy_ls, mp_prediction)
    mp_acc= accuracy_score(testy_ls, mp_prediction)
    # use back the sk method to calculate accuracy score
    # ts_acc = accuracy_score (testyidx_ls, ts_prediction_yidx_ls)

    # 4. summarize the classification methods
    print ('    Making summary of the classifiers...')
    if multinomialnb == 1:
        classifiers = ['GussianNB','BernoulliNB', 
        'MultinomialNB', 
        'Decision Tree', 'Random Forest', 'Logistic Regression' , 'SVM', 'KNN', 'MLP'
        # ,'Tensorflow'
        ]
        accuracy = np.array([nb_acc, bl_acc,
        mb_acc, 
        dtc_tree_acc, rfc_acc, l_acc, s_acc, knn_acc, mp_acc
        #  , ts_acc
        ])
    else:
        classifiers = ['GussianNB','BernoulliNB', 
        # 'MultinomialNB', 
        'Decision Tree', 'Random Forest', 'Logistic Regression' , 'SVM', 'KNN', 'MLP'
        # ,'Tensorflow'
        ]
        accuracy = np.array([nb_acc, bl_acc,
        # mb_acc, 
        dtc_tree_acc, rfc_acc, l_acc, s_acc, knn_acc, mp_acc
        #  , ts_acc
        ])        
    maxacc_idx = np.argmax(accuracy)
    # print(maxacc_idx)
    # print(classifiers)
    # print(accuracy)
    i=0
    for i in range(len(classifiers)):
        print(classifiers[i] + ": " + str(accuracy[i]))
    print('****************************************************')
    print(classifiers[maxacc_idx] + ' is with the highest accuracy.')
    print('****************************************************')

    if multinomialnb == 1:
        clfmethods=[nb_clf, bl_clf,
        mb_clf, 
        dtc_clf, rfc_clf, l_clf, s_clf, knn_clf, mp_clf
        #  , ts_clf
        ]
        clfpredictions=[nb_prediction, bl_prediction, 
        mb_prediction, 
        dtc_prediction, rfc_prediction, l_prediction, s_prediction, knn_prediction, mp_prediction
        # , ts_prediction
        ]
    else:
        clfmethods=[nb_clf, bl_clf,
        # mb_clf, 
        dtc_clf, rfc_clf, l_clf, s_clf, knn_clf, mp_clf
        #  , ts_clf
        ]
        clfpredictions=[nb_prediction, bl_prediction, 
        # mb_prediction, 
        dtc_prediction, rfc_prediction, l_prediction, s_prediction, knn_prediction, mp_prediction
        # , ts_prediction
        ]        

    clftestys=testy_ls
    # put all the results (methods, predictions, etc.) together
    clf_result_ls = [maxacc_idx, classifiers, clfmethods, clfpredictions, clftestys, accuracy]


    # rearrange the resut
    import math
    results_dict ={}
    i =-1
    for clfname in clf_result_ls[1]:
        i +=1
        results_dict[clfname]={}
        results_dict[clfname]['observed'] = list(clf_result_ls[4])
        results_dict[clfname]['predicted'] = list(clf_result_ls[3][i])
        results_dict[clfname]['clfmethod'] = clf_result_ls[2][i]
        tp=0
        tn=0
        fp=0
        fn=0
        j =-1
        for obs in results_dict[clfname]['observed']:
            j +=1
            pred = results_dict[clfname]['predicted'][j]
            # print(obs, pred)
            if (obs==1) & ( pred ==1):
                tp +=1
            elif (obs==0) & (pred == 0 ):
                tn +=1
            elif (obs==1) & ( pred==0 ):
                fn +=1
            elif (obs==0) & (pred == 1 ):
                fp +=1
        # print(244, clfname, tp, tn, fn, fp)
        results_dict[clfname]['metrics']={}
        results_dict[clfname]['metrics']['tp'] = tp
        results_dict[clfname]['metrics']['tn'] = tn
        results_dict[clfname]['metrics']['fn'] = fn
        results_dict[clfname]['metrics']['fp'] = fp
        if (tp+fp == 0):
            results_dict[clfname]['metrics']['ppv'] = 0
        else:
            results_dict[clfname]['metrics']['ppv'] = tp / (tp+fp) # rate of correct positve prediction

        if (tn+fn == 0):
            results_dict[clfname]['metrics']['npv'] = 0
        else:
            results_dict[clfname]['metrics']['npv'] = tn / (tn+fn) # rate of correct negative prediction

        if (tp + fn == 0):    
            results_dict[clfname]['metrics']['sensitivity'] = 0 # rate of identifying the positive cases
        else:
            results_dict[clfname]['metrics']['sensitivity'] = tp / (tp + fn) # rate of identifying the positive cases

        if (tn + fp == 0): 
            results_dict[clfname]['metrics']['specificity'] = 0
        else:
            results_dict[clfname]['metrics']['specificity'] = tn / (tn + fp) # rate of identifying the negative cases
        results_dict[clfname]['metrics']['accuracy'] = (tp+tn) / (tp+tn+fp+fn)
        # Matthews correction coefficient (mcc)
        # https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-019-6413-7
        if (tp+fp)*(tp+fn)*(tn+fp)*(tn+fn) == 0:
            results_dict[clfname]['metrics']['mcc'] = 0
        else:
            results_dict[clfname]['metrics']['mcc'] = ((tp*tn) - (fp*fn)) / math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
        # print(clfname, results_dict[clfname]['metrics'])
        # print ('===============accuracy_score', accuracy_score(results_dict[clfname]['observed'], results_dict[clfname]['predicted']))

    if make_cm_pngs == 1:
        # get the best method 
        # index_bestmethod=result[0]
        # thebestmethodname=result[1][index_bestmethod]
        # thebestclfmethod=result[2][index_bestmethod]
        # thebestprediction=result[3][index_bestmethod]
        # thebestactual=result[4][index_bestmethod]

        #5. plot confusion matrix of each classification
        print ('    Plot confusion matrices...')
        from sklearn.metrics import confusion_matrix

        # loop for each classificaiton
        i=0
        for i in range(len(classifiers)):
            bestaccmark=''
            if i == maxacc_idx:
                bestaccmark=' [best accuracy]'
            print(classifiers[i] + bestaccmark + ": accuracy = " + str(round(accuracy[i]*100,1)) + '%')
        
            # make confusion matrix
            cm = confusion_matrix(clftestys, clfpredictions[i])
            # # cm is a matrix like [[tn, fp][fn] [tp]] (the first row tells the specificity, the second sensitivity)

            #plot the heatmap
            # $ pip install matplotlib
            import matplotlib.pyplot as plt
            # $ pip install seaborn
            import seaborn as sns
            # import numpy as np

            # https://medium.com/@dtuk81/confusion-matrix-visualization-fc31e3f30fea
            # make lables for plot
            import numpy as np
            total = np.sum(cm)
            # calculate the percentage
            #  each row is 
                # rows= list(map(lambda x: x , cm))
                # in each row, the ele is
                    # ele = list(map(lambda e: e , row))
                    # instead of return element, return a % of that element in total
                    # elepct = list(map(lambda e: str(round(e/total*100, 1))+'%' , row))
            # now putting together
            labels = list(map(lambda x: list(map(lambda e: str(e) + ' (' + str(round(e/np.sum(x)*100, 1))+'%)' , x)) , cm))
            # print(labels)
            # plot it! Note: must have fmt=''
            sns.heatmap(cm, fmt='', center=True, annot=labels, cmap='Blues')

            print ('******* plot of confusion matrix ******')
            print ('(vertical: observed, horizontal: predicted)')        

            # save should go before plt.show() otherwise blank png is saved
            
            cfig = plt.gcf() # get the current figure
            # plt.show()
            # plt.draw()
            targetpng = targetpath + file_prefix +  classifiers[i] + '.png' 
            cfig.savefig(targetpng)
            plt.close(cfig) # must close it, otherwise the following plot will be drawn based on the existing plot (there will be two plots on the same figure)
        
    print ('******running classify_multi_methods is completed ******')

    if len(models) == 0:
        return nb_clf # rfc_clf
    elif models=='all':
        return results_dict
########## end ########################################################


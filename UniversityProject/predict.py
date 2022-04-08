import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as pdr
import datetime as dt
from keras.layers import Dense, Dropout, LSTM
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential

#Getting Data
def predict():
    crypto_currency = "BTC"
    against_currency = "GBP"

    start = dt.datetime(2016, 1, 1)
    end = dt.datetime.now()

    data = pdr.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', start, end)

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))
    prediction_days = 60

    x_train, y_train = [], []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    #Create NN

    model = Sequential()


    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=20))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))


    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)

    #Test

    test_start = dt.datetime(2020,1,1)+dt.timedelta(days=-prediction_days)
    test_end = dt.datetime.now()

    test_data = pdr.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', test_start, test_end)
    actual_price = test_data['Close'].values
    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

    model_input = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
    model_input = model_input.reshape(-1,1)
    model_input = scaler.fit_transform(model_input)

    x_test = []
    for x in range(prediction_days, len(model_input)):
        x_test.append(model_input[x-prediction_days:x, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    prediction_prices = model.predict(x_test)
    prediction_prices = scaler.inverse_transform(prediction_prices)

    plt.plot(actual_price, color='black', label='Actual Prices')
    plt.plot(prediction_prices, color='green', label='Predicted Prices')
    plt.title(f'{crypto_currency} price prediction')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    plt.show()

    #Predict

    real_data = [model_input[len(model_input) - prediction_days:len(model_input)+1, 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)
    return print(prediction)


if __name__ == '__main__':
    predict()
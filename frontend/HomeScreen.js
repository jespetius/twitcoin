import React, { useState, useEffect } from "react";
import {
  StyleSheet,
  Text,
  View,
  Button,
  ImageBackground,
  Alert,
  Image,
  TextInput,
  AsyncStorage,
} from "react-native";

// Fetch Sentiment analyse results via Flask

export default function HomeScreen() {
  const [value, onChangeText] = React.useState("");
  const [tweets, setTweets] = React.useState([]);
  const searchTweets = (event) => {
    event.preventDefault();
    const requestOptions = {
      method: "POST",
      body: JSON.stringify({ name: value }),
    };

    fetch("http://localhost:5000/json", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setTweets(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };
  console.log(tweets);

  return (
    <View style={styles.container}>
     <Image
        style={styles.tinyLogo}
        source={require('../images/logo.jpg')}
      />
      <TextInput
        style={styles.tInput}
        onChangeText={(text) => onChangeText(text)}
        value={value}
      />
      <View style={styles.buttons}>
        <Button onPress={searchTweets} title="Search" />
      </View>
      <Text style={styles.text2}>
        Type a search item and some AI magic will try to valuate its positivity
        using data from Twitter and the stock markets around the world.
      </Text>
      {tweets.map((tweet) => (
        <Text key={tweet.id}>{tweet.sentiment.nltk}</Text>
      ))}
      <Text style={styles.text2}>
        Average sentiment is{" "}
        {tweets.reduce((avg, value, _, { length }) => {
          return avg + value.sentiment.nltk / length;
        }, 0)}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white'
  },
  image: {
    flex: 1,
    resizeMode: "cover"
  },
  tinyLogo: {
    width: 300,
    height: 150,
    marginLeft: '38.5%'
  },
  buttons: {
    flexDirection: "row",
    justifyContent: "center",
  },
  tInput: {
    paddingVertical: 10,
    paddingHorizontal: 5,
    marginVertical: 10,
    borderRadius: 5,
    backgroundColor: "#ffffff70",
    borderColor: 'black',
    borderWidth: 1,
    textAlign: 'center',
    justifyContent: 'center',
    margin: 500
  },
  text2: {
    textAlign: 'center',
    padding: 25
  }
});

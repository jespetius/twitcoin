import React, { useState, useEffect } from "react";
import {
  StyleSheet,
  Text,
  View,
  Button,
  Alert,
  TextInput,
  AsyncStorage,
} from "react-native";

export default function HomeScreen() {
  const [value, onChangeText] = React.useState("");
  const [tweets, setTweets] = React.useState([]);
  const searchTweets = (event) => {
    console.log("Easter egg");
    event.preventDefault();
    const reqestOptions = {
      method: "POST",
      body: JSON.stringify({ name: value }),
    };

    fetch("http://localhost:5000/json", reqestOptions)
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
      <Text>Twitcoin</Text>
      <TextInput
        style={{ height: 40, borderColor: "gray", borderWidth: 1 }}
        onChangeText={(text) => onChangeText(text)}
        value={value}
      />
      <View style={styles.buttons}>
        <Button onPress={searchTweets} title="Search" />
      </View>
      <Text>
        Type a search item and some AI magic will try to valuate its positivity
        using data from Twitter and the stock markets around the world.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "blue",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "white",
  },
  tInput: {
    paddingVertical: 10,
    paddingHorizontal: 5,
    marginVertical: 10,
    borderRadius: 5,
    width: "50%",
    backgroundColor: "#ffffff70",
  },
  buttons: {
    flexDirection: "row",
    alignItems: "flex-start",
  },
});

import React, { useState, useEffect} from 'react';
import { StyleSheet, Text, View, Button, Alert, TextInput, AsyncStorage} from 'react-native';

export default function HomeScreen() {

 const [value, onChangeText] = React.useState('');

  return (
    <View style={styles.container}>
      <Text>Twitcoin</Text>
  <Text>A school project for analyzing Twitter trends and tweets and their relations with the current world.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'blue',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white'
  },
  tInput: {
    paddingVertical: 10,
    paddingHorizontal: 5,
    marginVertical: 10,
    borderRadius: 5,
    width: '50%',
    backgroundColor: '#ffffff70'
  },
  buttons: {
    flexDirection: 'row',
    alignItems: 'flex-start'
  },
});

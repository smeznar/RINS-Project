// Auto-generated. Do not edit!

// (in-package exercise2.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class moveRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.shape = null;
      this.time = null;
    }
    else {
      if (initObj.hasOwnProperty('shape')) {
        this.shape = initObj.shape
      }
      else {
        this.shape = '';
      }
      if (initObj.hasOwnProperty('time')) {
        this.time = initObj.time
      }
      else {
        this.time = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type moveRequest
    // Serialize message field [shape]
    bufferOffset = _serializer.string(obj.shape, buffer, bufferOffset);
    // Serialize message field [time]
    bufferOffset = _serializer.int32(obj.time, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type moveRequest
    let len;
    let data = new moveRequest(null);
    // Deserialize message field [shape]
    data.shape = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [time]
    data.time = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.shape.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'exercise2/moveRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4eb052c7f02dc3d6b175b629829c67f8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string shape
    int32 time
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new moveRequest(null);
    if (msg.shape !== undefined) {
      resolved.shape = msg.shape;
    }
    else {
      resolved.shape = ''
    }

    if (msg.time !== undefined) {
      resolved.time = msg.time;
    }
    else {
      resolved.time = 0
    }

    return resolved;
    }
};

class moveResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.lastShape = null;
    }
    else {
      if (initObj.hasOwnProperty('lastShape')) {
        this.lastShape = initObj.lastShape
      }
      else {
        this.lastShape = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type moveResponse
    // Serialize message field [lastShape]
    bufferOffset = _serializer.string(obj.lastShape, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type moveResponse
    let len;
    let data = new moveResponse(null);
    // Deserialize message field [lastShape]
    data.lastShape = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.lastShape.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'exercise2/moveResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'dcf2c8fef166172305df1e70a69819b8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string lastShape
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new moveResponse(null);
    if (msg.lastShape !== undefined) {
      resolved.lastShape = msg.lastShape;
    }
    else {
      resolved.lastShape = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: moveRequest,
  Response: moveResponse,
  md5sum() { return 'e107a27f216b950369e7480afd9738c6'; },
  datatype() { return 'exercise2/move'; }
};

// Auto-generated. Do not edit!

// (in-package lab1.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class Gps_data {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.latitude = null;
      this.longitude = null;
      this.altitude = null;
      this.utm_easting = null;
      this.utm_northing = null;
      this.zone = null;
      this.letter = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('latitude')) {
        this.latitude = initObj.latitude
      }
      else {
        this.latitude = 0.0;
      }
      if (initObj.hasOwnProperty('longitude')) {
        this.longitude = initObj.longitude
      }
      else {
        this.longitude = 0.0;
      }
      if (initObj.hasOwnProperty('altitude')) {
        this.altitude = initObj.altitude
      }
      else {
        this.altitude = 0.0;
      }
      if (initObj.hasOwnProperty('utm_easting')) {
        this.utm_easting = initObj.utm_easting
      }
      else {
        this.utm_easting = 0.0;
      }
      if (initObj.hasOwnProperty('utm_northing')) {
        this.utm_northing = initObj.utm_northing
      }
      else {
        this.utm_northing = 0.0;
      }
      if (initObj.hasOwnProperty('zone')) {
        this.zone = initObj.zone
      }
      else {
        this.zone = 0;
      }
      if (initObj.hasOwnProperty('letter')) {
        this.letter = initObj.letter
      }
      else {
        this.letter = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Gps_data
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [latitude]
    bufferOffset = _serializer.float64(obj.latitude, buffer, bufferOffset);
    // Serialize message field [longitude]
    bufferOffset = _serializer.float64(obj.longitude, buffer, bufferOffset);
    // Serialize message field [altitude]
    bufferOffset = _serializer.float64(obj.altitude, buffer, bufferOffset);
    // Serialize message field [utm_easting]
    bufferOffset = _serializer.float64(obj.utm_easting, buffer, bufferOffset);
    // Serialize message field [utm_northing]
    bufferOffset = _serializer.float64(obj.utm_northing, buffer, bufferOffset);
    // Serialize message field [zone]
    bufferOffset = _serializer.int64(obj.zone, buffer, bufferOffset);
    // Serialize message field [letter]
    bufferOffset = _serializer.string(obj.letter, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Gps_data
    let len;
    let data = new Gps_data(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [latitude]
    data.latitude = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [longitude]
    data.longitude = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [altitude]
    data.altitude = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [utm_easting]
    data.utm_easting = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [utm_northing]
    data.utm_northing = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [zone]
    data.zone = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [letter]
    data.letter = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += object.letter.length;
    return length + 52;
  }

  static datatype() {
    // Returns string type for a message object
    return 'lab1/Gps_data';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '51d4fcc0cdd0af9f1dda0d1d381f876e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    float64 latitude
    float64 longitude
    float64 altitude
    float64 utm_easting
    float64 utm_northing
    int64 zone
    string letter
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Gps_data(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.latitude !== undefined) {
      resolved.latitude = msg.latitude;
    }
    else {
      resolved.latitude = 0.0
    }

    if (msg.longitude !== undefined) {
      resolved.longitude = msg.longitude;
    }
    else {
      resolved.longitude = 0.0
    }

    if (msg.altitude !== undefined) {
      resolved.altitude = msg.altitude;
    }
    else {
      resolved.altitude = 0.0
    }

    if (msg.utm_easting !== undefined) {
      resolved.utm_easting = msg.utm_easting;
    }
    else {
      resolved.utm_easting = 0.0
    }

    if (msg.utm_northing !== undefined) {
      resolved.utm_northing = msg.utm_northing;
    }
    else {
      resolved.utm_northing = 0.0
    }

    if (msg.zone !== undefined) {
      resolved.zone = msg.zone;
    }
    else {
      resolved.zone = 0
    }

    if (msg.letter !== undefined) {
      resolved.letter = msg.letter;
    }
    else {
      resolved.letter = ''
    }

    return resolved;
    }
};

module.exports = Gps_data;

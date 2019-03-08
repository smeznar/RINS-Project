// Generated by gencpp from file exercise2/moveResponse.msg
// DO NOT EDIT!


#ifndef EXERCISE2_MESSAGE_MOVERESPONSE_H
#define EXERCISE2_MESSAGE_MOVERESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace exercise2
{
template <class ContainerAllocator>
struct moveResponse_
{
  typedef moveResponse_<ContainerAllocator> Type;

  moveResponse_()
    : lastShape()  {
    }
  moveResponse_(const ContainerAllocator& _alloc)
    : lastShape(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _lastShape_type;
  _lastShape_type lastShape;





  typedef boost::shared_ptr< ::exercise2::moveResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::exercise2::moveResponse_<ContainerAllocator> const> ConstPtr;

}; // struct moveResponse_

typedef ::exercise2::moveResponse_<std::allocator<void> > moveResponse;

typedef boost::shared_ptr< ::exercise2::moveResponse > moveResponsePtr;
typedef boost::shared_ptr< ::exercise2::moveResponse const> moveResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::exercise2::moveResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::exercise2::moveResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace exercise2

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::exercise2::moveResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::exercise2::moveResponse_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::exercise2::moveResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::exercise2::moveResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::exercise2::moveResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::exercise2::moveResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::exercise2::moveResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dcf2c8fef166172305df1e70a69819b8";
  }

  static const char* value(const ::exercise2::moveResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xdcf2c8fef1661723ULL;
  static const uint64_t static_value2 = 0x05df1e70a69819b8ULL;
};

template<class ContainerAllocator>
struct DataType< ::exercise2::moveResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "exercise2/moveResponse";
  }

  static const char* value(const ::exercise2::moveResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::exercise2::moveResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string lastShape\n\
\n\
";
  }

  static const char* value(const ::exercise2::moveResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::exercise2::moveResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.lastShape);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct moveResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::exercise2::moveResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::exercise2::moveResponse_<ContainerAllocator>& v)
  {
    s << indent << "lastShape: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.lastShape);
  }
};

} // namespace message_operations
} // namespace ros

#endif // EXERCISE2_MESSAGE_MOVERESPONSE_H
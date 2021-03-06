// Generated by gencpp from file exercise2/moveRequest.msg
// DO NOT EDIT!


#ifndef EXERCISE2_MESSAGE_MOVEREQUEST_H
#define EXERCISE2_MESSAGE_MOVEREQUEST_H


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
struct moveRequest_
{
  typedef moveRequest_<ContainerAllocator> Type;

  moveRequest_()
    : shape()
    , time(0)  {
    }
  moveRequest_(const ContainerAllocator& _alloc)
    : shape(_alloc)
    , time(0)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _shape_type;
  _shape_type shape;

   typedef int32_t _time_type;
  _time_type time;





  typedef boost::shared_ptr< ::exercise2::moveRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::exercise2::moveRequest_<ContainerAllocator> const> ConstPtr;

}; // struct moveRequest_

typedef ::exercise2::moveRequest_<std::allocator<void> > moveRequest;

typedef boost::shared_ptr< ::exercise2::moveRequest > moveRequestPtr;
typedef boost::shared_ptr< ::exercise2::moveRequest const> moveRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::exercise2::moveRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::exercise2::moveRequest_<ContainerAllocator> >::stream(s, "", v);
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
struct IsFixedSize< ::exercise2::moveRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::exercise2::moveRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::exercise2::moveRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::exercise2::moveRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::exercise2::moveRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::exercise2::moveRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::exercise2::moveRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "4eb052c7f02dc3d6b175b629829c67f8";
  }

  static const char* value(const ::exercise2::moveRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x4eb052c7f02dc3d6ULL;
  static const uint64_t static_value2 = 0xb175b629829c67f8ULL;
};

template<class ContainerAllocator>
struct DataType< ::exercise2::moveRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "exercise2/moveRequest";
  }

  static const char* value(const ::exercise2::moveRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::exercise2::moveRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string shape\n\
int32 time\n\
";
  }

  static const char* value(const ::exercise2::moveRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::exercise2::moveRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.shape);
      stream.next(m.time);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct moveRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::exercise2::moveRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::exercise2::moveRequest_<ContainerAllocator>& v)
  {
    s << indent << "shape: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.shape);
    s << indent << "time: ";
    Printer<int32_t>::stream(s, indent + "  ", v.time);
  }
};

} // namespace message_operations
} // namespace ros

#endif // EXERCISE2_MESSAGE_MOVEREQUEST_H

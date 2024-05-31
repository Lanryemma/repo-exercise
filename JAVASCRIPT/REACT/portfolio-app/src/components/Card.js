import { Heading, HStack, Image, Text, VStack } from "@chakra-ui/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import React from "react";

const Card = ({ title, description, imageSrc }) => {
  // Implement the UI for the Card component according to the instructions.
  // You should be able to implement the component with the elements imported above.
  // Feel free to import other UI components from Chakra UI if you wish to.
  
  return (
    <HStack>
       <VStack justifyContent="start"
          alignItems="start"
          backgroundColor="white"
          style={{borderRadius: '10px'}} >
          <Image src={imageSrc} style={{borderRadius: '10px'}}/>
          <VStack justifyContent="start" alignItems="start" style={{padding: '10px', fontFamily: 'Didact Gothic'}}>
            <Heading as='h6' color='black'style={{fontSize: 'large'}}>{title}</Heading>
            <Text color="gray" style={{fontSize: 'small'}}>{description}</Text>
            <HStack>
              <Text color='black'>See more</Text>
              <FontAwesomeIcon icon={faArrowRight}  color='black' size="1x" />
            </HStack>
          </VStack>
          
       </VStack>
    </HStack>
  );
};

export default Card;

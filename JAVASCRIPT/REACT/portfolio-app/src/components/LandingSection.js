import React from "react";
import { Avatar, Heading, VStack } from "@chakra-ui/react";
import FullScreenSection from "./FullScreenSection";

const greeting = "Hello, I am Pete!";
const bio1 = "A frontend developer";
const bio2 = "specialised in React";
const Url = "https://i.pravatar.cc/150?img=7"

// Implement the UI for the LandingSection component according to the instructions.
// Use a combination of Avatar, Heading and VStack components.
const LandingSection = () => (
  <FullScreenSection
    justifyContent="center"
    alignItems="center"
    isDarkBackground
    backgroundColor="#2A4365"
  >
  <VStack>
    <Avatar  height= '80px' width="80px">
      <img src={Url} style={{clipPath: "circle(50% at 50% 50%)"}}/>
    </Avatar>
    <p>{greeting}</p>
    <Heading as='h2' size='2xl'>
      {bio1}
    </Heading>
    <Heading as='h2' size='2xl'>
      {bio2}
    </Heading>
  </VStack>
  </FullScreenSection>
);

export default LandingSection;

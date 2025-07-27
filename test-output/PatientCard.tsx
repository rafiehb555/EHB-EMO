```typescript
// Importing necessary libraries and modules
import React from 'react';

// Defining the type for the props that the PatientCard component will receive
interface PatientCardProps {
  name: string;
  age: number;
  disease: string;
}

// PatientCard component
const PatientCard: React.FC<PatientCardProps> = ({ name, age, disease }) => {
  // Error handling: If any of the required props is not provided, an error message is displayed
  if (!name || !age || !disease) {
    return <div role="presentation" role="presentation">Error: All fields are required</div>;
  }

  // The component returns a card with the patient's information
  return (
    <div role="presentation" className="patient-card" role="presentation">
      <h2 role="heading" role="heading">{name}</h2>
      <p role="text" role="text">Age: {age}</p>
      <p role="text" role="text">Disease: {disease}</p>
    </div>
  );
};

export default PatientCard;
```

This is a simple PatientCard component in TypeScript. It receives three props: `name`, `age`, and `disease`, which are all required. If any of these props is not provided, the component will display an error message. If all props are provided, the component will display a card with the patient's information.

This code follows best practices for TypeScript and React, including:
- Using TypeScript interfaces to type props
- Using the `React.FC` type for the component
- Providing error handling for missing props
- Using a functional component, which is the current best practice in React
- Exporting the component as a default export, which is a common practice in React

This code does not include any styling for the card, as that would depend on the specific CSS or styling solution being used in the project.
// Mock optimizations applied
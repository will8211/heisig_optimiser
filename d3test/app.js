// Updated app.js

// Set canvas dimensions
const canvasWidth = 1200;
const canvasHeight = 800;

// Sample data structure
const data = {
  number: "44",
  character: "占",
  keyword: "tell fortunes",
  level: "Medium",
  id: "G",
  requirements: [
    {
      number: "43",
      character: "卜",
      keyword: "divination",
      level: null,
      id: "E",
      requirements: [
        {
          number: null,
          character: "丨",
          keyword: "walking stick",
          level: null,
          id: "C",
          requirements: [
            {
              number: "1",
              character: "一",
              keyword: "one",
              level: "Elementary",
              id: "B",
              requirements: [],
            },
          ],
        },
        {
          number: null,
          character: "丶",
          keyword: "a drop of",
          level: null,
          id: "D",
          requirements: [],
        },
      ],
    },
    {
      number: "11",
      character: "口",
      keyword: "mouth",
      level: "Elementary",
      id: "F",
      requirements: [],
    },
  ],
};

// Convert the data into a hierarchy
const hierarchyData = d3.hierarchy(data, (d) => d.requirements);

// Create a tree layout with specified dimensions
const treeLayout = d3.tree().size([canvasHeight, canvasWidth - 160]); // Adjust width for margin

// Apply the tree layout to the hierarchy data
const treeData = treeLayout(hierarchyData);

// Extract nodes and links from the tree data
const nodes = treeData.descendants();
const links = treeData.links();

// Select the body element and append an SVG container
const mainSvg = d3
  .select("body")
  .append("svg")
  .attr("width", canvasWidth)
  .attr("height", canvasHeight);

// Adjust the mainSvg to add some margins
mainSvg.attr("transform", "translate(80,0)"); // Shift right to allow for text and margin

// Create links using the tree data
const link = mainSvg
  .selectAll(".link")
  .data(links)
  .enter()
  .append("path")
  .attr("class", "link")
  .attr(
    "d",
    d3
      .linkHorizontal()
      .x((d) => d.y)
      .y((d) => d.x)
  );

// Create nodes
const node = mainSvg
  .selectAll(".node")
  .data(nodes)
  .enter()
  .append("g")
  .attr("class", "node")
  .attr("transform", (d) => `translate(${d.y},${d.x})`);

// Append circles for nodes with improved styling
node
  .append("circle")
  .attr("r", 10)
  .style("fill", "#69b3a2") // Light green fill
  .style("stroke", "#406d80") // Darker stroke for contrast

// Append labels for nodes with original styling
// Adjust label styling to ensure normal font weight and set font family
// Adjust label styling to use a lighter font weight
node.append("text")
  .attr("dy", 3)
  .attr("x", (d) => (d.children ? -15 : 15))
  .style("text-anchor", (d) => (d.children ? "end" : "start"))
  .text((d) => `${d.data.character}\n${d.data.keyword} (${d.data.number})`);

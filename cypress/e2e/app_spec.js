describe('Página de Opiniones', () => {
  it('Carga y muestra las opiniones en la página principal', () => {
    // Visitar la página principal
    cy.visit('/')
    // Verificar que se muestren al menos una tarjeta de opinión
    cy.get('[data-cy="review-card"]').should('have.length.greaterThan', 0)
  })
}) 